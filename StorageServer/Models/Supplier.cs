using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace StorageServer.Models;

public class Supplier
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    [MaxLength(60)]
    public required string CompanyName { get; set; }

    [MaxLength(16)]
    public string? Phone { get; set; }

    public string? Address { get; set; }

    [MaxLength(30)]
    public string? Email { get; set; }

    public required virtual ICollection<Supply> Supplies { get; set; }

    [ForeignKey(nameof(AppUser))]
    public required string AppUserId { get; set; }

    public required AppUser AppUser { get; set; }
}
