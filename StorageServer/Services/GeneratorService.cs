using Bogus;

using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

using StorageServer.Models;

namespace StorageServer.Services;

public class GeneratorService(
    UserManager<AppUser> userManager,
    AppDbContext dbContext,
    IPasswordHasher<AppUser> passwordHasher
)
{
    private readonly UserManager<AppUser> _userManager = userManager;
    private readonly AppDbContext _dbContext = dbContext;
    private readonly IPasswordHasher<AppUser> _passwordHasher = passwordHasher;

    public async Task<ICollection<AppUser>> GenerateUsersAsync(int count = 1)
    {
        var userFaker = new Faker<AppUser>()
            .RuleFor(u => u.UserName, f => f.Internet.UserName())
            .RuleFor(u => u.IsStaff, false)
            .RuleFor(u => u.PasswordHash, (_, u) =>
                _passwordHasher.HashPassword(u, "123456789"));

        var users = userFaker.Generate(count);

        await _dbContext.AddRangeAsync(users);
        await _dbContext.SaveChangesAsync();

        return users;
    }

    public async Task<ICollection<Customer>> GenerateCustomerAsync(int count = 1)
    {
        var users = await GenerateUsersAsync(count);

        var customerFaker = new Faker<Customer>()
            .RuleFor(c => c.CompanyName, f => f.Company.CompanyName())
            .RuleFor(c => c.Phone, f => f.Phone.PhoneNumber("+7 (###) ###-##-##"))
            .RuleFor(c => c.Address, f => f.Address.FullAddress())
            .RuleFor(c => c.Email, f => f.Internet.Email());

        var customers = new List<Customer>
        {
            Capacity = count
        };

        customers = customerFaker.Generate(count);

        foreach (var (customer, user) in customers.Zip(users))
        {
            customer.AppUserId = user.Id;
        }

        await _dbContext.Customers.AddRangeAsync(customers);
        await _dbContext.SaveChangesAsync();

        return customers;
    }

    public async Task<ICollection<Supplier>> GenerateSupplierAsync(int count = 1)
    {
        var users = await GenerateUsersAsync(count);

        var supplierFaker = new Faker<Supplier>()
            .RuleFor(s => s.CompanyName, f => f.Company.CompanyName())
            .RuleFor(s => s.Phone, f => f.Phone.PhoneNumber("+7 (###) ###-##-##"))
            .RuleFor(s => s.Address, f => f.Address.FullAddress())
            .RuleFor(s => s.Email, f => f.Internet.Email());

        var suppliers = new List<Supplier>
        {
            Capacity = count
        };

        suppliers = supplierFaker.Generate(count);

        foreach (var (supplier, user) in suppliers.Zip(users))
        {
            supplier.AppUserId = user.Id;
        }

        await _dbContext.Suppliers.AddRangeAsync(suppliers);
        await _dbContext.SaveChangesAsync();

        return suppliers;
    }

    public async Task<ICollection<Product>> GenerateProductAsync(
        int count = 1,
        decimal minPrice = 1,
        decimal maxPrice = 1000
    )
    {
        var productFaker = new Faker<Product>()
            .RuleFor(p => p.ProductName, f => f.Commerce.ProductName())
            .RuleFor(p => p.Price, f => Math.Round(f.Random.Decimal(minPrice, maxPrice), 2));

        var products = productFaker.Generate(count);

        await _dbContext.Products.AddRangeAsync(products);
        await _dbContext.SaveChangesAsync();

        return products;
    }

    public async Task<ICollection<Sale>> GenerateSalesAsync(
        DateTimeOffset minDate,
        DateTimeOffset maxDate,
        int count = 1
    )
    {
        var customerIds = await _dbContext.Customers
            .Select(c => c.Id)
            .ToListAsync();

        if (!customerIds.Any())
            throw new InvalidOperationException("Нет покупателей");

        var productIds = await _dbContext.Products
            .Select(p => p.Id)
            .ToListAsync();

        if (!productIds.Any())
            throw new InvalidOperationException("Нет товаров");

        var sales = new List<Sale>();
        var allSaleUnits = new List<SaleUnit>();

        var saleFaker = new Faker<Sale>()
            .RuleFor(s => s.CustomerId, f => f.PickRandom(customerIds))
            .RuleFor(s => s.PlannedDate, f => f.Date.BetweenOffset(minDate, maxDate))
            .RuleFor(s => s.RealDate, (f, s) =>
            {
                var minRealDate = s.PlannedDate.AddDays(-10);
                var maxRealDate = s.PlannedDate.AddDays(10);

                var actualMin = minRealDate < minDate ? minDate : minRealDate;
                var actualMax = maxRealDate > maxDate ? maxDate : maxRealDate;

                return f.Date.BetweenOffset(actualMin, actualMax);
            });

        var saleUnitFaker = new Faker<SaleUnit>()
            .RuleFor(su => su.Amount, f => f.Random.Int(1, 100))
            .RuleFor(su => su.ProductId, f => f.PickRandom(productIds))
            .RuleFor(su => su.Price, f => Math.Round(f.Random.Decimal(10, 5000), 2));

        for (int i = 0; i < count; i++)
        {
            var sale = saleFaker.Generate();

            var unitCount = new Faker().Random.Int(1, 30);
            var saleUnits = saleUnitFaker.Generate(unitCount);

            foreach (var unit in saleUnits)
            {
                unit.Sales.Add(sale);
            }

            sale.SaleUnits = saleUnits;

            sales.Add(sale);
            allSaleUnits.AddRange(saleUnits);
        }

        await _dbContext.Sales.AddRangeAsync(sales);
        await _dbContext.SaleUnits.AddRangeAsync(allSaleUnits);
        await _dbContext.SaveChangesAsync();

        return sales;
    }

    public async Task<ICollection<Supply>> GenerateSuppliesAsync(
        DateTimeOffset minDate,
        DateTimeOffset maxDate,
        int count = 1
    )
    {
        var supplierIds = await _dbContext.Suppliers
            .Select(s => s.Id)
            .ToListAsync();

        if (!supplierIds.Any())
            throw new InvalidOperationException("Нет поставщиков");

        var productIds = await _dbContext.Products
            .Select(p => p.Id)
            .ToListAsync();

        if (!productIds.Any())
            throw new InvalidOperationException("Нет товаров");

        var supplies = new List<Supply>();
        var allSupplyUnits = new List<SupplyUnit>();

        var supplyFaker = new Faker<Supply>()
            .RuleFor(s => s.SupplierId, f => f.PickRandom(supplierIds))
            .RuleFor(s => s.PlannedDate, f => f.Date.BetweenOffset(minDate, maxDate))
            .RuleFor(s => s.RealDate, (f, s) =>
            {
                var minRealDate = s.PlannedDate.AddDays(-10);
                var maxRealDate = s.PlannedDate.AddDays(10);

                var actualMin = minRealDate < minDate ? minDate : minRealDate;
                var actualMax = maxRealDate > maxDate ? maxDate : maxRealDate;

                return f.Date.BetweenOffset(actualMin, actualMax);
            });

        var supplyUnitFaker = new Faker<SupplyUnit>()
            .RuleFor(su => su.Amount, f => f.Random.Int(1, 100))
            .RuleFor(su => su.ProductId, f => f.PickRandom(productIds))
            .RuleFor(su => su.Price, f => Math.Round(f.Random.Decimal(10, 5000), 2));

        for (int i = 0; i < count; i++)
        {
            var supply = supplyFaker.Generate();

            var unitCount = new Faker().Random.Int(1, 30);
            var supplyUnits = supplyUnitFaker.Generate(unitCount);

            foreach (var unit in supplyUnits)
            {
                unit.Supplies.Add(supply);
            }

            supply.SupplyUnits = supplyUnits;

            supplies.Add(supply);
            allSupplyUnits.AddRange(supplyUnits);
        }

        await _dbContext.Supplies.AddRangeAsync(supplies);
        await _dbContext.SupplyUnits.AddRangeAsync(allSupplyUnits);
        await _dbContext.SaveChangesAsync();

        return supplies;
    }
}