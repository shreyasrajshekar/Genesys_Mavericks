using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;


namespace DRYRUN.Models
{
    [Table("system_metrics")]
    public class SystemMetric : BaseModel
    {
        [PrimaryKey("id", false)]
        public int Id { get; set; }

        [Column("cpu_usage")]
        public float CpuUsage { get; set; }

        [Column("ram_usage_percent")]
        public double RamUsagePercent { get; set; }

        [Column("green_score")]
        public int GreenScore { get; set; }

        [Column("mobile_connected")]
        public bool IsMobileConnected { get; set; }

        [Column("mobile_battery")]
        public float MobileBatteryLevel { get; set; }

        [Column("created_at")] // Useful for time-series charts
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }
}