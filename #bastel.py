import requests

using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main()
    {
        var url = "https://maps.infas-lt.de";
        using (var client = new HttpClient())
        {
            // HEAD request
            var headRequest = new HttpRequestMessage(HttpMethod.Head, url);
            var headResponse = await client.SendAsync(headRequest);
            Console.WriteLine(headResponse);

            // GET request
            var getResponse = await client.GetAsync(url);
            Console.WriteLine(getResponse);
        }
    }
}