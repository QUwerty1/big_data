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
    UserManager<AppUser> userManager,
    AppDbContext appDbContext,
    MapperService mapperService
) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        return user!.IsStaff == false 
            ? Forbid() 
            : Ok(appDbContext.Supplies
                .Include(s => s.SupplyUnits)
                .Select(mapperService.ToDto));
    }

    [HttpGet("{supply_id}")]
    public async Task<IActionResult> Get([FromRoute] int supply_id)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        var supply = appDbContext.Supplies
            .Where(s => s.Id == supply_id)
            .Include(s => s.SupplyUnits)
            .FirstOrDefault();

        return supply == null 
            ? NotFound() 
            : Ok(mapperService.ToDto(supply));
    }

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] SupplyDto supplyDto)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        await appDbContext.AddAsync(mapperService.ToEntity(supplyDto));
        await appDbContext.SaveChangesAsync();

        return Ok();
    }

    [HttpPut]
    public async Task<IActionResult> Update([FromBody] SupplyDto supplyDto)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        var oldSupply = await appDbContext.Sales
            .Where(s => s.Id == supplyDto.Id)
            .Include(s => s.SaleUnits)
            .FirstOrDefaultAsync();

        if (oldSupply == null)
            return NotFound();

        appDbContext.RemoveRange(oldSupply.SaleUnits);
        
        var newSupply = mapperService.ToEntity(supplyDto);

        appDbContext.Update(newSupply);
        await appDbContext.SaveChangesAsync();

        return Ok();
    }
}
