using cp2020.Models;
using LiteDB;
using System;
using System.Collections.Generic;

namespace cp2020.DAL
{
    /// <summary>
    /// Общий репозиторий для работы с базой данных
    /// </summary>
    public class DbRepository
    {
        private LiteDatabase _liteDb;

        public DbRepository(LiteDbContext liteDbContext)
        {
            _liteDb = liteDbContext.Database;
        }

        public IEnumerable<Doc> Doc_FindAll()
        {
            return _liteDb.GetCollection<Doc>()
            .FindAll();
        }

        public Guid Doc_Insert(Doc doc)
        {
            return _liteDb.GetCollection<Doc>().Insert(doc);
        }
    }
}
