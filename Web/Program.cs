using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;

namespace cp2020
{
    /// <summary>
    /// Класс для точки входа в приложение
    /// </summary>
    public class Program
    {
        public static void Main(string[] args)
        {
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                });
    }
}
