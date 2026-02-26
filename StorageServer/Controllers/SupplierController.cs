using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using StorageServer.Models;

namespace StorageServer.Controllers;

[Route("supplier")]
[ApiController]
[Authorize]
public class SupplierController(
    AppDbContext appDbContext,
    UserManager<AppUser> userManager
) : ControllerBase
{
    [HttpGet("{supplier_id}")]
    public async Task<IActionResult> GetCuStomerInfo([FromRoute] int supplier_id)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        var supplier = await appDbContext.Suppliers
            .Where(s => s.Id == supplier_id)
            .FirstOrDefaultAsync();

        if (supplier == null)
            return NotFound();

        return Ok(new SupplierDTOStaff(
            supplier.Id,
            supplier.CompanyName,
            supplier.Phone,
            supplier.Address,
            supplier.Email,
            supplier.AppUserId
        ));
    }

    [HttpPost]
    public async Task<IActionResult> CreateSupplier([FromBody] SupplierDTO supplierDTO)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (await appDbContext.Suppliers.Where(c => c.AppUserId == user!.Id).AnyAsync())
            return Conflict("Аккаунт покупателя уже существует");

        var supplier = new Supplier
        {
            CompanyName = supplierDTO.CompanyName,
            Phone = supplierDTO.Phone,
            Address = supplierDTO.Address,
            Email = supplierDTO.Email,
            Supplies = [],
            AppUserId = user!.Id,
            AppUser = user
        };

        await appDbContext.Suppliers.AddAsync(supplier);
        await appDbContext.SaveChangesAsync();

        return Created();
    }

    [HttpGet]
    public async Task<IActionResult> Get()
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.Supplier == null)
            return NotFound();

        var supplier = user.Supplier;

        return Ok(new SupplierDTO(
            supplier.CompanyName,
            supplier.Phone,
            supplier.Address,
            supplier.Email
        ));
    }

    [HttpGet("all")]
    public async Task<IActionResult> GetAll([FromQuery] int? take, [FromQuery] int skip = 0)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        var suppliers = appDbContext.Suppliers.Skip(skip);

        if (take != null)
        {
            suppliers.Take(take ?? 0);
        }

        return Ok(suppliers.Select(c => new SupplierDTOStaff(
            c.Id, c.CompanyName, c.Phone, c.Address, c.Email, c.AppUserId
        )));
    }
}

public record SupplierDTO(
    string CompanyName,
    string Phone,
    string Address,
    string Email
);

public record SupplierDTOStaff(
    int Id,
    string CompanyName,
    string Phone,
    string Address,
    string Email,
    string AppUserId
);