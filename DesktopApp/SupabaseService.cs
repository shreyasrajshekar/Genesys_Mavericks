using Supabase;

namespace DRYRUN
{
    public class SupabaseService
    {
        private readonly Client _client;

        public SupabaseService(string url, string key)
        {
            var options = new SupabaseOptions { AutoRefreshToken = true };
            _client = new Client(url, key, options);
        }

        public async Task Initialize() => await _client.InitializeAsync();

        public async Task SaveMetrics(Models.SystemMetric metric)
        {
            await _client.From<Models.SystemMetric>().Insert(metric);
        }
    }
}