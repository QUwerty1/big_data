using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using StorageServer.Dto;
using StorageServer.Models;
using StorageServer.Services;

namespace StorageServer.Controllers;

[Route("supplier")]
[ApiController]
[Authorize]
public class SupplierController(
    AppDbContext appDbContext,
    MapperService mapperService,
    UserManager<AppUser> userManager
) : ControllerBase
{
    [HttpGet("{supplier_id}")]
    [Authorize(Policy = "IsStaff")]
    [ProducesResponseType<CustomerDto>(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Get([FromRoute] int supplier_id)
    {
        var supplier = await appDbContext.Suppliers
            .Where(s => s.Id == supplier_id)
            .Include(s => s.Supplies)
            .FirstOrDefaultAsync();

        return supplier == null
            ? NotFound()
            : Ok(mapperService.ToDto(supplier));
    }

    [HttpPost]
    [ProducesResponseType(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public async Task<IActionResult> Create([FromBody] NewSupplier newSupplier)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (await appDbContext.Customers.Where(c => c.AppUserId == user!.Id).AnyAsync())
            return Conflict("Аккаунт покупателя уже существует");

        var supplier = new Supplier
        {
            AppUserId = user!.Id,
            Phone = newSupplier.Phone,
            Email = newSupplier.Email,
            Address = newSupplier.Address,
            CompanyName = newSupplier.CompanyName
        };

        await appDbContext.Suppliers.AddAsync(supplier);
        await appDbContext.SaveChangesAsync();

        return Created();
    }

    [HttpGet("me")]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType<CustomerDto>(StatusCodes.Status200OK)]
    public async Task<IActionResult> Get()
    {
        var supplier = await appDbContext.Suppliers
            .Where(s => s.AppUser.UserName == User.Identity!.Name)
            .Include(s => s.Supplies)
            .FirstOrDefaultAsync();

        return supplier == null 
            ? NotFound() 
            : Ok(mapperService.ToDto(supplier));
    }

    [HttpGet]
    [Authorize(Policy = "IsStaff")]
    [ProducesResponseType<CustomerDto>(StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAll([FromQuery] int? take, [FromQuery] int skip = 0)
    {
        var suppliers = appDbContext.Suppliers.OrderBy(s => s.Id).Skip(skip);

        if (take != null)
            suppliers.Take(take ?? 0);

        return Ok(suppliers
            .Include(s => s.Supplies)
            .Select(mapperService.ToDto));
    }

    // [HttpGet("me")]
    // public async Task<IActionResult> GetMe()
    // {
    //     var user = await userManager.FindByNameAsync(User.Identity!.Name!);
    //     var supplier = await appDbContext.Suppliers
    //         .Include(s => s.Supplies)
    //         .ThenInclude(supply => supply.SupplyUnits)
    //         .Where(s => s.AppUserId == user!.Id)
    //         .FirstOrDefaultAsync();

    //     if (supplier == null)
    //     {
    //         return NotFound();
    //     }

    //     return Ok(supplier.Supplies.Select(mapperService.ToDto));
    // }
}

public record NewSupplier(
    string CompanyName,
    string Phone,
    string Address,
    string Email
);