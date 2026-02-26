using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace StorageServer.Models;

public class Product
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    [MaxLength(30)]
    public required string ProductName { get; set; }

    [MaxLength(30)]
    public required string CategoryName { get; set; }

    [MaxLength(10)]
    public required string Units { get; set; }

    [Column(TypeName = "money")]
    public decimal Price { get; set; }

    public required virtual ICollection<SaleUnit> SaleUnits { get; set; }
    public required virtual ICollection<SupplyUnit> SupplyUnits { get; set; }
}