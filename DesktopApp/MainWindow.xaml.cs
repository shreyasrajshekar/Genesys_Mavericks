using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media;

namespace DRYRUN
{
    public partial class MainWindow : Window
    {
        private SystemMonitor monitor;
        public ObservableCollection<SystemAlert> SystemLog { get; set; } = new ObservableCollection<SystemAlert>();

        public MainWindow()
        {
            InitializeComponent();
            monitor = new SystemMonitor();
            AlertFeedControl.ItemsSource = SystemLog;
            StartDeepScan();
        }

        // MainWindow.xaml.cs
        private async void StartDeepScan()
        {
            // Initialize Supabase only once
            await monitor.InitializeAsync();

            while (true)
            {
                // Collect metrics
                await monitor.CollectData();

                // ===== PC METRICS =====
                CpuText.Text = $"{monitor.CpuUsage}%";
                CpuBar.Value = monitor.CpuUsage;
                RamText.Text = $"{monitor.RamUsagePercent}%";
                RamBar.Value = monitor.RamUsagePercent;
                PcBatteryText.Text = $"{monitor.BatteryLevel}%";
                PcBatteryBar.Value = monitor.BatteryLevel;
                PcWearLabel.Text = $"WEAR: {monitor.BatteryWearPercent:F1}%";

                // ===== GREEN SCORE =====
                GreenScoreText.Text = $"{monitor.GreenScore}%";
                GreenScoreBar.Value = monitor.GreenScore;

                // ===== MOBILE METRICS =====
                if (monitor.IsMobileConnected)
                {
                    MobileDataContainer.Opacity = 1.0;
                    AdbWaitText.Visibility = Visibility.Collapsed;

                    MobileLevelText.Text = $"{monitor.MobileBatteryLevel}%";
                    MobileHealthText.Text = monitor.MobileBatteryHealth.ToUpper();
                    MobileTempText.Text = $"{monitor.MobileBatteryTemp:F1}°C";
                    MobileNetText.Text = monitor.MobileNetwork.ToUpper();
                    MobileStoreText.Text = $"{monitor.MobileStorageUsed}%";
                    MobileRamText.Text = $"{monitor.MobileRamUsage:F1} GB";
                    MobileRamBar.Value = monitor.MobileRamPercent;

                    // Mobile-only Green Score
                    int mobileScore = monitor.CalculateMobileGreenScore();
                    MobileGreenScoreText.Text = $"{mobileScore}%";
                    MobileGreenScoreBar.Value = mobileScore;
                }
                else
                {
                    MobileDataContainer.Opacity = 0.2;
                    AdbWaitText.Visibility = Visibility.Visible;

                    MobileGreenScoreText.Text = "-";
                    MobileGreenScoreBar.Value = 0;
                }

                // ===== REFRESH LOG =====
                SystemLog.Clear();
                foreach (string sug in monitor.Suggestions)
                {
                    var parts = sug.Split(new[] { ':' }, 2);
                    SystemLog.Add(new SystemAlert
                    {
                        AlertMessage = parts[0].Trim().ToUpper() + ":",
                        SuggestionText = parts.Length > 1 ? parts[1].Trim() : ""
                    });
                }

                await Task.Delay(2000);
            }
        }

        private void Window_MouseDown(object sender, MouseButtonEventArgs e) { if (e.LeftButton == MouseButtonState.Pressed) DragMove(); }
        private void Close_Click(object sender, RoutedEventArgs e) => System.Windows.Application.Current.Shutdown();
        private void Minimize_Click(object sender, RoutedEventArgs e) => this.WindowState = WindowState.Minimized;
    }

    public class SystemAlert
    {
        public string AlertMessage { get; set; }
        public string SuggestionText { get; set; }
    }
}