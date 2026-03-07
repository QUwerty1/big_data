using Microsoft.EntityFrameworkCore;

namespace StorageServer.Models;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Customer> Customers { get; set; }
    public DbSet<Product> Products { get; set; }
    public DbSet<Sale> Sales { get; set; }
    public DbSet<SaleUnit> SaleUnits { get; set; }
    public DbSet<Supplier> Suppliers { get; set; }
    public DbSet<Supply> Supplies { get; set; }
    public DbSet<SupplyUnit> SupplyUnits { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
    }
}