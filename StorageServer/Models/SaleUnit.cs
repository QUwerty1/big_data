using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace StorageServer.Models;

public class SaleUnit
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    public int Amount { get; set; }

    public int ProductId { get; set; }

    public required virtual Product Product { get; set; }

    [Column(TypeName = "money")]
    public decimal Price { get; set; }

    public required virtual ICollection<Sale> Sales { get; set; }
}