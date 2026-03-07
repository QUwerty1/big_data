using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace StorageServer.Models;

public class Sale
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    public int CustomerId { get; set; }

    public DateTimeOffset RealDate { get; set; }

    public DateTimeOffset PlannedDate { get; set; }

    public virtual ICollection<SaleUnit> SaleUnits { get; set; } = [];
}