using Microsoft.VisualBasic.Devices;
using Supabase;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Management;
using System.Text;
using System.Threading.Tasks;

namespace DRYRUN
{

    public class SystemMonitor
    {
        private readonly PerformanceCounter cpuCounter;
        private readonly PerformanceCounter ramCounter;
        private readonly string supabaseUrl = "https://tfjrgpdsacjcmoeilldt.supabase.co";
        private readonly string supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRmanJncGRzYWNqY21vZWlsbGR0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEwNzMzNzYsImV4cCI6MjA4NjY0OTM3Nn0.80xPt7HmPfnaJha6bPJEZvcRL9P6-yynQnuhxyYKqfg";
        private Supabase.Client supabase;

        // ================= GREEN SYSTEM =================
        private int greenPoints = 0;
        private int dailyPointsEarned = 0;
        private const int MaxDailyPoints = 50;
        private DateTime lastPointAwardDate = DateTime.Today;

        // ================= PC BATTERY =================
        private readonly Queue<(float level, DateTime time)> batteryHistory = new();
        private const int historyMaxCount = 12;

        // ================= MOBILE =================
        public bool IsMobileConnected { get; private set; }
        public bool IsUsbUnstable { get; private set; }

        public float MobileBatteryLevel { get; private set; } = -1f;
        public float MobileBatteryTemp { get; private set; } = 0f;
        public float MobileBatteryVoltage { get; private set; } = 0f;
        public string MobileBatteryHealth { get; private set; } = "Unknown";

        public float MobileCpuUsage { get; private set; }
        public float MobileRamUsage { get; private set; }
        public float MobileRamPercent { get; private set; }
        public float MobileStorageUsed { get; private set; }
        public string MobileNetwork { get; private set; } = "Offline";

        // ================= PC METRICS =================
        public float CpuUsage { get; private set; }
        public double RamUsagePercent { get; private set; }
        public float BatteryLevel { get; private set; }
        public float BatteryWearPercent { get; private set; }
        public int GreenScore { get; private set; }
        public int BonusPoints => greenPoints;

        private int usbDisconnectCount = 0;
        private DateTime lastUsbCheck = DateTime.MinValue;

        private readonly StringBuilder logBuilder = new();
        public string GetLog() => logBuilder.ToString();

        // Suggestions
        public List<string> Suggestions { get; private set; } = new();

        public SystemMonitor()
        {

            cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
            ramCounter = new PerformanceCounter("Memory", "Available MBytes");
            cpuCounter.NextValue();
            var options = new SupabaseOptions { AutoRefreshToken = true };
            supabase = new Supabase.Client(supabaseUrl, supabaseKey, options);
        }
        public async Task InitializeAsync()
        {
            await supabase.InitializeAsync();
        }
        public async Task PushMetricsToCloud()
        {
            try
            {
                var metric = new Models.SystemMetric
                {
                    CpuUsage = this.CpuUsage,
                    RamUsagePercent = this.RamUsagePercent,
                    GreenScore = this.GreenScore,
                    IsMobileConnected = this.IsMobileConnected,
                    MobileBatteryLevel = this.MobileBatteryLevel
                };

                // Capture the response to see if there is an error
                var response = await supabase.From<Models.SystemMetric>().Insert(metric);
                var errorText = await response.ResponseMessage.Content.ReadAsStringAsync();
                Console.WriteLine($"Supabase insert failed: {errorText}");
                if (response.ResponseMessage.IsSuccessStatusCode)
                    Console.WriteLine("Data pushed successfully!");
                else
                    Console.WriteLine($"Error: {response.ResponseMessage.ReasonPhrase}");   
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Critical Error: {ex.Message}");
            }
        }

        // =========================================================
        public async Task CollectData()
        {
            Suggestions.Clear();

            await UpdateCpu();
            UpdateRam();
            AnalyzeBattery();

            CheckMobileConnection();
            DetectUsbInstability();

            if (IsMobileConnected)
            {
                GetMobileBatteryInfo();
                GetMobileCpuInfo();
                GetMobileRamInfo();
                GetMobileStorageInfo();
                GetMobileNetworkInfo();
            }
            else
            {
                ResetMobileValues();
            }

            bool deviceErrorDetected = CheckDeviceErrors();
            GreenScore = CalculateGreenScore(deviceErrorDetected);
            AwardDailyPoints();
            GenerateSuggestions(deviceErrorDetected);
            LogStatus();
        }

        // ================= CPU =================
        private async Task UpdateCpu()
        {
            await Task.Delay(500);
            CpuUsage = (float)Math.Round(cpuCounter.NextValue(), 1);
        }

        // ================= RAM =================
        private void UpdateRam()
        {
            ComputerInfo ci = new ComputerInfo();
            double totalRamMb = ci.TotalPhysicalMemory / (1024.0 * 1024.0);
            double availableMb = ramCounter.NextValue();

            double usedPercent = ((totalRamMb - availableMb) / totalRamMb) * 100;
            RamUsagePercent = Math.Round(usedPercent, 1);
        }
        private void GenerateRamSuggestions()
        {
            try
            {
                // 1. Get all processes and immediately filter out System/Idle to avoid permission errors
                // 2. We use 'using System.Linq;' for OrderByDescending
                var topProcesses = System.Diagnostics.Process.GetProcesses()
                    .Where(p => {
                        try { return p.Id > 4 && !string.IsNullOrEmpty(p.ProcessName); }
                        catch { return false; } // Filter out processes we can't even touch
                    })
                    .OrderByDescending(p => {
                        try { return p.WorkingSet64; }
                        catch { return 0; }
                    })
                    .Take(5)
                    .ToList();

                if (topProcesses.Count == 0)
                {
                    Suggestions.Add($"High RAM usage ({RamUsagePercent:F1}%): Close unused apps.");
                    return;
                }

                foreach (var proc in topProcesses)
                {
                    try
                    {
                        string appName = proc.ProcessName;
                        long ramMb = proc.WorkingSet64 / (1024 * 1024);

                        // Now it catches devenv (Visual Studio), Chrome, etc.
                        if (ramMb > 500)
                            Suggestions.Add($"HIGH CONSUMPTION: {appName} is consuming {ramMb} MB.");
                        else
                            Suggestions.Add($"SUGGESTION: Close Tabs or Refresh Environments");
                    }
                    catch
                    {
                        // If a process closes while we are reading it, just skip it
                        continue;
                    }
                }
            }
            catch
            {
                Suggestions.Add($"RAM high ({RamUsagePercent:F1}%): Analyze Task Manager.");
            }
        }
        // ================= BATTERY =================
        private float maxObservedCharge = -1f; // start uninitialized

        private void AnalyzeBattery()
        {
            try
            {
                // Current battery level
                var battery = System.Windows.Forms.SystemInformation.PowerStatus;
                float currentLevel = (float)Math.Round(battery.BatteryLifePercent * 100f, 1);
                BatteryLevel = currentLevel;

                // Add to history
                batteryHistory.Enqueue((BatteryLevel, DateTime.Now));
                if (batteryHistory.Count > historyMaxCount)
                    batteryHistory.Dequeue();

                // Initialize maxObservedCharge on first run
                if (maxObservedCharge < 0f)
                    maxObservedCharge = currentLevel + 5f; // initially assume 5% wear

                // Update maxObservedCharge if we see a higher full charge
                if (currentLevel > maxObservedCharge)
                    maxObservedCharge = currentLevel;

                // Calculate battery wear based on difference from max observed
                BatteryWearPercent = (float)Math.Round(maxObservedCharge - currentLevel, 1);

                // Clamp between 5% and 100%
                BatteryWearPercent = Math.Clamp(BatteryWearPercent, 5f, 100f);
            }
            catch
            {
                BatteryWearPercent = 5f; // fallback minimum wear
            }
        }


        // ================= ADB =================
        private string RunAdbCommand(string arguments)
        {
            try
            {
                ProcessStartInfo psi = new ProcessStartInfo
                {
                    FileName = "adb",
                    Arguments = arguments,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using (Process process = Process.Start(psi))
                {
                    string output = process.StandardOutput.ReadToEnd();
                    process.WaitForExit();
                    return output;
                }
            }
            catch
            {
                return null;
            }
        }

        private void CheckMobileConnection()
        {
            string output = RunAdbCommand("devices");

            if (string.IsNullOrWhiteSpace(output))
            {
                IsMobileConnected = false;
                return;
            }

            IsMobileConnected = output
                .Split('\n')
                .Any(line => line.Trim().EndsWith("device"));
        }

        private void DetectUsbInstability()
        {
            // Avoid checking too frequently
            if (DateTime.Now - lastUsbCheck < TimeSpan.FromSeconds(10))
                return;

            lastUsbCheck = DateTime.Now;

            // Increment counter if mobile disconnected
            if (!IsMobileConnected)
            {
                usbDisconnectCount++;
            }
            else
            {
                // Reset counter on successful connection
                usbDisconnectCount = 0;
            }

            // Flag as unstable if disconnected 3+ times in a row
            IsUsbUnstable = usbDisconnectCount >= 3;
        }
        private void ResetMobileValues()
        {
            MobileBatteryLevel = -1f;
            MobileBatteryTemp = 0f;
            MobileBatteryVoltage = 0f;
            MobileBatteryHealth = "Unknown";

            MobileCpuUsage = 0f;
            MobileRamUsage = 0f;
            MobileRamPercent = 0f;
            MobileStorageUsed = 0f;
            MobileNetwork = "Offline";
        }

        // ================= MOBILE INFO =================
        public void GetMobileBatteryInfo()
        {
            try
            {
                // Reset values
                MobileBatteryLevel = -1f;
                MobileBatteryTemp = 0f;
                MobileBatteryVoltage = 0f;
                MobileBatteryHealth = "Unknown";

                string output = RunAdbCommand("shell dumpsys battery");
                if (string.IsNullOrEmpty(output)) return;

                foreach (var rawLine in output.Split('\n'))
                {
                    var line = rawLine.Trim().ToLower();

                    // Battery level
                    if (line.StartsWith("level:") && float.TryParse(line.Replace("level:", "").Trim(), out float level))
                        MobileBatteryLevel = level;

                    // Battery temperature
                    if (line.StartsWith("temperature:") && float.TryParse(line.Replace("temperature:", "").Trim(), out float temp))
                        MobileBatteryTemp = temp / 10f; // Convert to °C

                    // Battery voltage
                    if (line.StartsWith("voltage:") && float.TryParse(line.Replace("voltage:", "").Trim(), out float voltage))
                        MobileBatteryVoltage = voltage / 1000f; // Convert to volts

                    // Standard health field
                    if (line.StartsWith("health:") && int.TryParse(new string(line.Where(char.IsDigit).ToArray()), out int health))
                    {
                        MobileBatteryHealth = health switch
                        {
                            1 => "Unknown",
                            2 => "Good",
                            3 => "Overheat",
                            4 => "Dead",
                            5 => "Overvoltage",
                            6 => "Failure",
                            7 => "Cold",
                            _ => "Unknown"
                        };
                    }

                    // Samsung / OEM Battery SOH
                    if (line.StartsWith("msavedbatterybsoh:") || line.StartsWith("msavedbatterymaxbsoh:"))
                    {
                        string valueStr = line.Split(':')[1].Trim();
                        if (float.TryParse(valueStr, out float soh))
                            MobileBatteryHealth = $"{soh:F1}%"; // Show as percentage
                    }
                }

                // Fallback: risk-based estimate if still unknown
                if (MobileBatteryHealth == "Unknown")
                {
                    if (MobileBatteryTemp > 40 || MobileBatteryLevel < 20)
                        MobileBatteryHealth = "At Risk";
                    else
                        MobileBatteryHealth = "Good";
                }
            }
            catch
            {
                ResetMobileValues();
            }
        }
        public async Task SyncToSupabase(SupabaseService service)
        {
            var data = new Models.SystemMetric
            {
                CpuUsage = this.CpuUsage,
                RamUsagePercent = this.RamUsagePercent,
                GreenScore = this.GreenScore,
                IsMobileConnected = this.IsMobileConnected,
                MobileBatteryLevel = this.MobileBatteryLevel
            };

            await service.SaveMetrics(data);
        }
        public void GetMobileCpuInfo()
        {
            string output = RunAdbCommand("shell dumpsys cpuinfo");
            if (string.IsNullOrEmpty(output)) return;

            var totalLine = output.Split('\n').FirstOrDefault(l => l.ToLower().Contains("total"));
            if (totalLine != null)
            {
                string digits = new string(totalLine.Split('%')[0].Where(char.IsDigit).ToArray());
                if (float.TryParse(digits, out float cpu))
                    MobileCpuUsage = cpu;
            }
        }

        public void GetMobileRamInfo()
        {
            string output = RunAdbCommand("shell cat /proc/meminfo");
            if (string.IsNullOrEmpty(output)) return;

            float totalKb = 0f, availableKb = 0f;

            foreach (var line in output.Split('\n'))
            {
                if (line.StartsWith("MemTotal"))
                    totalKb = ExtractKb(line);
                if (line.StartsWith("MemAvailable"))
                    availableKb = ExtractKb(line);
            }

            if (totalKb > 0)
            {
                float usedKb = totalKb - availableKb;
                MobileRamUsage = (float)Math.Round(usedKb / 1024f, 1);
                MobileRamPercent = (float)Math.Round((usedKb / totalKb) * 100f, 1);
            }
        }

        public void GetMobileStorageInfo()
        {
            string output = RunAdbCommand("shell df /data");
            if (string.IsNullOrEmpty(output)) return;

            var lines = output.Split('\n');
            if (lines.Length > 1)
            {
                var parts = lines[1].Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                if (parts.Length >= 5 && float.TryParse(parts[4].Replace("%", ""), out float storage))
                    MobileStorageUsed = storage;
            }
        }

        public void GetMobileNetworkInfo()
        {
            string output = RunAdbCommand("shell dumpsys connectivity");
            if (string.IsNullOrEmpty(output))
            {
                MobileNetwork = "Offline";
                return;
            }

            if (output.ToLower().Contains("wifi"))
                MobileNetwork = "WiFi";
            else if (output.ToLower().Contains("mobile"))
                MobileNetwork = "Mobile Data";
            else
                MobileNetwork = "Unknown";
        }

        private float ExtractKb(string line)
        {
            string digits = new string(line.Where(char.IsDigit).ToArray());
            return float.TryParse(digits, out float value) ? value : 0f;
        }

        // ================= GREEN SCORE =================
        public int CalculateGreenScore(bool deviceError)
        {
            // ===== PC Metrics =====
            double cpuImpact = (CpuUsage / 100.0) * 30;             // max 30 points
            double ramImpact = (RamUsagePercent / 100.0) * 25;      // max 25 points
            double batteryImpact = (BatteryWearPercent / 100.0) * 15; // max 15 points
            double errorImpact = deviceError ? 15 : 0;             // max 15 points

            // ===== Mobile Metrics =====
            double mobileBatteryImpact = 0;
            double mobileRamImpact = 0;
            double mobileTempImpact = 0;
            double mobileNetworkImpact = 0;

            if (IsMobileConnected)
            {
                // Battery low -> bigger penalty
                mobileBatteryImpact = MobileBatteryLevel < 20
                    ? 10
                    : (MobileBatteryLevel < 50 ? 5 : 0);

                // Mobile RAM high usage
                mobileRamImpact = MobileRamPercent > 80
                    ? 5
                    : 0;

                // Mobile temperature high
                mobileTempImpact = MobileBatteryTemp > 45
                    ? 5
                    : 0;

                // Mobile network offline
                mobileNetworkImpact = MobileNetwork == "Offline" ? 5 : 0;
            }

            // Total deduction
            double totalDeduction = cpuImpact + ramImpact + batteryImpact + errorImpact
                                    + mobileBatteryImpact + mobileRamImpact
                                    + mobileTempImpact + mobileNetworkImpact;

            // Clamp and return
            int greenScore = (int)Math.Max(100 - totalDeduction, 0);
            return greenScore;
        }

        public int CalculateMobileGreenScore()
        {
            double batteryImpact = 0;
            double ramImpact = 0;
            double tempImpact = 0;
            double networkImpact = 0;

            if (IsMobileConnected)
            {
                batteryImpact = MobileBatteryLevel < 20 ? 40 :
                                (MobileBatteryLevel < 50 ? 20 : 0);

                ramImpact = MobileRamPercent > 80 ? 30 : 0;
                tempImpact = MobileBatteryTemp > 45 ? 20 : 0;
                networkImpact = MobileNetwork == "Offline" ? 10 : 0;
            }

            double totalDeduction = batteryImpact + ramImpact + tempImpact + networkImpact;
            return (int)Math.Max(100 - totalDeduction, 0);
        }

        private void AwardDailyPoints()
        {
            if (lastPointAwardDate.Date != DateTime.Today)
            {
                dailyPointsEarned = 0;
                lastPointAwardDate = DateTime.Today;
            }

            if (dailyPointsEarned < MaxDailyPoints)
            {
                greenPoints += 5;
                dailyPointsEarned += 5;
            }
        }

        public bool CheckDeviceErrors()
        {
            try
            {
                var searcher = new ManagementObjectSearcher("SELECT * FROM Win32_PnPEntity");
                foreach (var device in searcher.Get())
                    if (device["ConfigManagerErrorCode"] != null && Convert.ToInt32(device["ConfigManagerErrorCode"]) != 0)
                        return true;
            }
            catch { }

            return false;
        }

        // ================= SUGGESTIONS =================
        private void GenerateSuggestions(bool deviceError)
        {
            Suggestions.Clear();

            // ---------- CPU ----------
            if (CpuUsage > 70)
                Suggestions.Add($"High CPU usage ({CpuUsage:F1}%): close unused programs or check background tasks.");

            // ---------- RAM ----------
            if (RamUsagePercent > 70)
                GenerateRamSuggestions();

            // ---------- PC Battery ----------
            if (BatteryWearPercent > 20)
                Suggestions.Add($"Battery wear is high ({BatteryWearPercent:F1}%): consider calibrating or replacing the battery.");

            // ---------- Device Errors ----------
            if (deviceError)
                Suggestions.Add("Device errors detected: check Device Manager for faulty devices or drivers.");

            // ---------- USB ----------
            if (IsUsbUnstable)
            {
                if (!IsMobileConnected)
                    Suggestions.Add("⚠ Mobile disconnected multiple times: possible faulty USB cable or port. Check your connection.");
                else
                    Suggestions.Add("⚠ USB instability detected: mobile connected but intermittent issues. Try a different cable or port.");
            }

            // ---------- Mobile ----------
            if (MobileBatteryTemp > 40)
                Suggestions.Add($"Mobile temperature high ({MobileBatteryTemp:F1}°C): avoid heavy apps or charging while hot.");
            if (MobileBatteryLevel < 20 & MobileBatteryLevel > 0)
                Suggestions.Add($"Mobile battery low ({MobileBatteryLevel:F1}%): charge soon.");
            if (MobileBatteryLevel < 0 )
                Suggestions.Add("");

            if (MobileRamPercent > 80)
                Suggestions.Add($"Mobile RAM usage high ({MobileRamPercent:F1}%): close unused apps to improve performance.");
            if (MobileStorageUsed > 90)
                Suggestions.Add($"Mobile storage almost full ({MobileStorageUsed:F1}%): clear cache or remove unused files.");
            if (MobileNetwork == "Offline")
                Suggestions.Add("Mobile network offline: Phone might not be connected");
        }


        private void LogStatus()
        {
            logBuilder.AppendLine($"CPU: {CpuUsage:F1}% | RAM: {RamUsagePercent:F1}% | Battery Wear: {BatteryWearPercent:F1}%");
            logBuilder.AppendLine($"Green Score: {GreenScore} | Bonus Points: {greenPoints}");

            if (IsMobileConnected)
                logBuilder.AppendLine($"Mobile: {MobileBatteryLevel}% | Temp: {MobileBatteryTemp:F1}°C | RAM: {MobileRamPercent:F1}% | Storage: {MobileStorageUsed}% | Network: {MobileNetwork}");
            else
                logBuilder.AppendLine("Mobile: Not Connected");

            if (Suggestions.Count > 0)
            {
                logBuilder.AppendLine("Suggestions:");
                foreach (var suggestion in Suggestions)
                    logBuilder.AppendLine($"- {suggestion}");
            }

            logBuilder.AppendLine("--------------------------------");

            if (logBuilder.Length > 8000)
                logBuilder.Clear();
        }
    }
}
