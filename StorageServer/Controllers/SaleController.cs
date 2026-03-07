using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using StorageServer.Dto;
using StorageServer.Models;
using StorageServer.Services;

namespace StorageServer.Controllers;

[Route("sale")]
[ApiController]
[Authorize]
public class SaleController(
    UserManager<AppUser> userManager,
    AppDbContext appDbContext,
    MapperService mapperService
) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        return Ok(appDbContext.Sales.Include(su => su.SaleUnits).Select(mapperService.ToDto));
    }

    [HttpGet("{sale_id}")]
    public async Task<IActionResult> Get([FromRoute] int sale_id)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        var sale = appDbContext.Sales
            .Where(s => s.Id == sale_id)
            .Include(s => s.SaleUnits)
            .FirstOrDefault();

        if (sale == null)
            return NotFound();

        return Ok(mapperService.ToDto(sale));
    }

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] SaleDto saleDto)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        await appDbContext.AddAsync(mapperService.ToEntity(saleDto));
        await appDbContext.SaveChangesAsync();

        return Ok();
    }

    [HttpPut]
    public async Task<IActionResult> Update([FromBody] SaleDto saleDto)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        var oldSale = await appDbContext.Sales
            .Where(s => s.Id == saleDto.Id)
            .Include(s => s.SaleUnits)
            .FirstOrDefaultAsync();

        if (oldSale == null)
            return NotFound();

        appDbContext.RemoveRange(oldSale.SaleUnits);
        
        var newSale = mapperService.ToEntity(saleDto);

        appDbContext.Update(newSale);
        await appDbContext.SaveChangesAsync();

        return Ok();
    }
}
