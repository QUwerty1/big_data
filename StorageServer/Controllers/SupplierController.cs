using Microsoft.AspNetCore.Authorization;
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
    MapperService mapperService
) : ControllerBase
{
    [HttpGet("{supplier_id}")]
    [Authorize(Policy = "IsStaff")]
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
    [Authorize(Policy = "IsStaff")]
    public async Task<IActionResult> Create([FromBody] SupplierDto supplierDto)
    {
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
    [Authorize(Policy = "IsStaff")]
    public async Task<IActionResult> GetAll([FromQuery] int? take, [FromQuery] int skip = 0)
    {
        var suppliers = appDbContext.Suppliers.Skip(skip);

        if (take != null)
            suppliers.Take(take ?? 0);

        return Ok(suppliers.Include(s => s.Supplies).Select(mapperService.ToDto));
    }
}