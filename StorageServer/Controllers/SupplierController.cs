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
    UserManager<AppUser> userManager,
    MapperService mapperService
) : ControllerBase
{
    [HttpGet("{supplier_id}")]
    public async Task<IActionResult> Get([FromRoute] int supplier_id)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        var supplier = await appDbContext.Suppliers
            .Where(s => s.Id == supplier_id)
            .Include(s => s.Supplies)
            .FirstOrDefaultAsync();

        return supplier == null
            ? NotFound()
            : Ok(mapperService.ToDto(supplier));
    }

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] SupplierDto supplierDto)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (await appDbContext.Suppliers.Where(c => c.AppUserId == user!.Id).AnyAsync())
            return Conflict("Аккаунт покупателя уже существует");

        await appDbContext.Suppliers.AddAsync(mapperService.ToEntity(supplierDto));
        await appDbContext.SaveChangesAsync();

        return Created();
    }

    [HttpGet("me")]
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
    public async Task<IActionResult> GetAll([FromQuery] int? take, [FromQuery] int skip = 0)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        var suppliers = appDbContext.Suppliers.Skip(skip);

        if (take != null)
            suppliers.Take(take ?? 0);

        return Ok(suppliers.Include(s => s.Supplies).Select(mapperService.ToDto));
    }
}