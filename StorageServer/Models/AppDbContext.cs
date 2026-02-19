using Microsoft.EntityFrameworkCore;

namespace StorageServer.Models;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Customer> Customers {get;set;}
    public DbSet<Product> Products {get;set;}
    public DbSet<Sale> Sales {get;set;}
    public DbSet<SaleUnit> SaleUnits {get;set;}
    // public DbSet<SaleUnitSale> SaleUnitSales {get;set;}
}
