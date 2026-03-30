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
        return Ok(appDbContext.Sales.Include(su => su.SaleUnits).Select(mapperService.ToDto));
    }

    [HttpGet("{sale_id}")]
    [Authorize(Policy = "IsStaff")]
    [ProducesResponseType<SaleDto>(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
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
    [ProducesResponseType(StatusCodes.Status201Created)]
    public async Task<IActionResult> Create([FromBody] SaleDto saleDto)
    {
        await appDbContext.AddAsync(mapperService.ToEntity(saleDto));
        await appDbContext.SaveChangesAsync();

        return Created();
    }

    [HttpPut]
    [Authorize(Policy = "IsStaff")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
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

    [HttpGet("me")]
    public async Task<IActionResult> GetMe()
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);
        var customer = await appDbContext.Customers
            .Include(c => c.Sales)
            .ThenInclude(sale => sale.SaleUnits)
            .Where(c => c.AppUserId == user!.Id)
            .FirstOrDefaultAsync();

        if (customer == null)
        {
            return NotFound();
        }

        return Ok(customer.Sales.Select(mapperService.ToDto));
    }
}
