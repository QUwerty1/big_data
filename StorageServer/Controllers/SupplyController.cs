using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using StorageServer.Dto;
using StorageServer.Models;
using StorageServer.Services;

namespace StorageServer.Controllers;

[Route("supply")]
[ApiController]
[Authorize]
public class SupplyController(
    AppDbContext appDbContext,
    MapperService mapperService,
    UserManager<AppUser> userManager
) : ControllerBase
{
    [HttpGet]
    [Authorize(Policy = "IsStaff")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAll()
    {
        return Ok(appDbContext.Supplies
            .Include(s => s.SupplyUnits)
            .Select(mapperService.ToViewDto));
    }

    [HttpGet("{supply_id}")]
    [ProducesResponseType<SupplyDto>(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status403Forbidden)]
    public async Task<IActionResult> Get([FromRoute] int supply_id)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user == null)
            return NotFound();

        if (user.IsStaff)
        {
            var supply = appDbContext.Supplies
                .Where(s => s.Id == supply_id)
                .Include(s => s.SupplyUnits)
                .FirstOrDefault();

            if (supply == null)
                return NotFound();

            return Ok(mapperService.ToDto(supply));
        }

        var supplier = await appDbContext.Suppliers
            .Where(s => s.AppUserId == user.Id)
            .FirstOrDefaultAsync();

        if (supplier == null)
            return NotFound();

        var supplyForSupplier = appDbContext.Supplies
            .Where(s => s.Id == supply_id && s.SupplierId == supplier.Id)
            .Include(s => s.SupplyUnits)
            .FirstOrDefault();

        if (supplyForSupplier == null)
            return NotFound();

        return Ok(mapperService.ToDto(supplyForSupplier));
    }

    [HttpPost]
    [Authorize(Policy = "IsStaff")]
    [ProducesResponseType(StatusCodes.Status201Created)]
    public async Task<IActionResult> Create([FromBody] SupplyDto supplyDto)
    {
        await appDbContext.AddAsync(mapperService.ToEntity(supplyDto));
        await appDbContext.SaveChangesAsync();

        return Created();
    }

    [HttpPut]
    [Authorize(Policy = "IsStaff")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Update([FromBody] SupplyDto supplyDto)
    {
        var supply = await appDbContext.Supplies
            .Where(s => s.Id == supplyDto.Id)
            .Include(s => s.SupplyUnits)
            .FirstOrDefaultAsync();

        if (supply == null)
            return NotFound();

        appDbContext.RemoveRange(supply.SupplyUnits);

        var newSupplyUnits = supplyDto.SupplyUnits.Select(mapperService.ToEntity).ToArray();

        supply.SupplierId = supplyDto.SupplierId;
        supply.PlannedDate = supplyDto.PlannedDate;
        supply.RealDate = supplyDto.RealDate;
        supply.SupplyUnits = newSupplyUnits;

        await appDbContext.SaveChangesAsync();

        return Ok();
    }
}
