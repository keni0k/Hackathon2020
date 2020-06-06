using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using cp2020.Models;
using cp2020.DAL;

namespace cp2020.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly DbRepository _repository;

        public HomeController(ILogger<HomeController> logger, DbRepository repository)
        {
            _logger = logger;
            _repository = repository;


            var t = repository.Doc_FindAll().ToList();
            var t3 = repository.Doc_Insert(new Doc
            {
                Text = "test1"
            });
            var t2 = repository.Doc_FindAll();
            
            foreach(var tt in t)
            {
                var i = 0;
            }

            foreach (var tt in t2)
            {
                var i = 0;

            }
        }

        public IActionResult Index()
        {
            return View();
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
