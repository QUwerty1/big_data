using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace StorageServer.Models;

public class Sale
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    public int CustomerId { get; set; }
    
    public required virtual Customer Customer { get; set; }

    public DateTimeOffset RealDate { get; set; }

    [MaxLength(9)]
    public required string SaleType { get; set; }

    public DateTimeOffset PlannedDate { get; set; }

    public required ICollection<SaleUnit> SaleUnits { get; set; }
}
