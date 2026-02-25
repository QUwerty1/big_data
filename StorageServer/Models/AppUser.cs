using Microsoft.AspNetCore.Identity;

namespace StorageServer.Models;

public class AppUser : IdentityUser
{
    public Customer? Customer { get; set; }
    public Supplier? Supplier { get; set; }
    public bool IsStaff { get; set; } = false;
}
