using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace StorageServer.Models;

public class SaleUnit
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    public int Amount { get; set; }

    public int ProductId { get; set; }

    public virtual Product Product { get; set; } = null!;

    [Column(TypeName = "money")]
    public decimal Price { get; set; }

    public virtual ICollection<Sale> Sales { get; set; } = [];
}