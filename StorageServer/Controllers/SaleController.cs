using Microsoft.AspNetCore.Authorization;
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
    AppDbContext appDbContext,
    MapperService mapperService
) : ControllerBase
{
    [HttpGet]
    [Authorize(Policy = "IsStaff")]
    public async Task<IActionResult> GetAll()
    {
        return Ok(appDbContext.Sales.Include(su => su.SaleUnits).Select(mapperService.ToDto));
    }

    [HttpGet("{sale_id}")]
    [Authorize(Policy = "IsStaff")]
    public async Task<IActionResult> Get([FromRoute] int sale_id)
    {
        var sale = appDbContext.Sales
            .Where(s => s.Id == sale_id)
            .Include(s => s.SaleUnits)
            .FirstOrDefault();

        if (sale == null)
            return NotFound();

        return Ok(mapperService.ToDto(sale));
    }

    [HttpPost]
    [Authorize(Policy = "IsStaff")]
    public async Task<IActionResult> Create([FromBody] SaleDto saleDto)
    {
        await appDbContext.AddAsync(mapperService.ToEntity(saleDto));
        await appDbContext.SaveChangesAsync();

        return Ok();
    }

    [HttpPut]
    [Authorize(Policy = "IsStaff")]
    public async Task<IActionResult> Update([FromBody] SaleDto saleDto)
    {
        var sale = await appDbContext.Sales
            .Where(s => s.Id == saleDto.Id)
            .Include(s => s.SaleUnits)
            .FirstOrDefaultAsync();

        if (sale == null)
            return NotFound();

        appDbContext.RemoveRange(sale.SaleUnits);
        
        var newSaleUnits = saleDto.SaleUnits.Select(mapperService.ToEntity).ToArray();

        sale.CustomerId = saleDto.CustomerId;
        sale.RealDate = saleDto.RealDate;
        sale.PlannedDate = saleDto.PlannedDate;
        sale.SaleUnits = newSaleUnits;

        await appDbContext.SaveChangesAsync();

        return Ok();
    }
}
