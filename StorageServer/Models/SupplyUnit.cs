using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace StorageServer.Models;

public class SupplyUnit
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    public int Amount { get; set; }

    public required Product Product { get; set; }

    [Column(TypeName = "money")]
    public required decimal Price { get; set; }

    public required virtual ICollection<Supply> Supplies { get; set; }
}