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

    [MaxLength(20)]
    public required string Phone { get; set; }

    public required string Address { get; set; }

    [MaxLength(60)]
    public required string Email { get; set; }

    public virtual ICollection<Supply> Supplies { get; set; } = [];

    [ForeignKey(nameof(AppUser))]
    public required string AppUserId { get; set; }

    public virtual AppUser AppUser { get; set; } = null!;
}