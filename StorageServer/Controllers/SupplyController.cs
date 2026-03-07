using Microsoft.AspNetCore.Authorization;
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
    MapperService mapperService
) : ControllerBase
{
    [HttpGet]
    [Authorize(Policy = "IsStaff")]
    public async Task<IActionResult> GetAll()
    {
        return Ok(appDbContext.Supplies
            .Include(s => s.SupplyUnits)
            .Select(mapperService.ToDto));
    }

    [HttpGet("{supply_id}")]
    [Authorize(Policy = "IsStaff")]
    public async Task<IActionResult> Get([FromRoute] int supply_id)
    {
        var supply = appDbContext.Supplies
            .Where(s => s.Id == supply_id)
            .Include(s => s.SupplyUnits)
            .FirstOrDefault();

        return supply == null 
            ? NotFound() 
            : Ok(mapperService.ToDto(supply));
    }

    [HttpPost]
    [Authorize(Policy = "IsStaff")]
    public async Task<IActionResult> Create([FromBody] SupplyDto supplyDto)
    {
        await appDbContext.AddAsync(mapperService.ToEntity(supplyDto));
        await appDbContext.SaveChangesAsync();

        return Ok();
    }

    [HttpPut]
    [Authorize(Policy = "IsStaff")]
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
