using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace StorageServer.Models;

public class Supply
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    public int SupplierId { get; set; }
    
    public required Supplier Supplier { get; set; }

    public DateTimeOffset RealDate { get; set; }

    public DateTimeOffset PlannedDate { get; set; }

    public required virtual ICollection<SupplyUnit> SupplyUnits { get; set; }
}
