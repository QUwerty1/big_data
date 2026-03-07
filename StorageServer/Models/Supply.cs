using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace StorageServer.Models;

public class Supply
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    public int SupplierId { get; set; }

    public virtual Supplier Supplier { get; set; } = null!;

    public DateTimeOffset RealDate { get; set; }

    public DateTimeOffset PlannedDate { get; set; }

    public virtual ICollection<SupplyUnit> SupplyUnits { get; set; } = [];
}