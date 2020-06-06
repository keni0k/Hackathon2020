using System;

namespace cp2020.Models
{
    /// <summary>
    /// Сущность "Документ"
    /// </summary>
    public class Doc
    {
        public Guid Id { get; set; }

        /// <summary>
        /// Текст документа
        /// </summary>
        public string Text { get; set; }
    }
}
