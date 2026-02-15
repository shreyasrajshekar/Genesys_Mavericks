using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public class N8nService
{
    private readonly HttpClient _httpClient;
    private readonly string _webhookUrl;

    public N8nService(string webhookUrl)
    {
        _httpClient = new HttpClient();
        _webhookUrl = webhookUrl;
    }

    public async Task<bool> SendDataAsync(object payload)
    {
        try
        {
            var json = JsonSerializer.Serialize(payload);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync(_webhookUrl, content);
            response.EnsureSuccessStatusCode();

            var responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine("n8n Response: " + responseBody);
            return true;
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error sending to n8n: " + ex.Message);
            return false;
        }
    }
}
