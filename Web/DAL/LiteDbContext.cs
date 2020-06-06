using LiteDB;
using Microsoft.Extensions.Configuration;

namespace cp2020.DAL
{
    /// <summary>
    /// Контекст базы данных
    /// </summary>
    public class LiteDbContext
    {
        public LiteDatabase Database { get; }

        public LiteDbContext(IConfiguration configuration)
        {
            Database = new LiteDatabase(configuration["ConnectionStrings:LiteDB"]);
        }
    }
}
