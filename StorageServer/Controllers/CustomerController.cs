using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using StorageServer.Dto;
using StorageServer.Models;
using StorageServer.Services;

namespace StorageServer.Controllers;

[Route("customer")]
[ApiController]
[Authorize]
public class CustomerController(
    AppDbContext appDbContext,
    UserManager<AppUser> userManager,
    MapperService mapperService
) : ControllerBase
{
    [HttpGet("{customer_id}")]
    [Authorize(Policy = "IsStaff")]
    [ProducesResponseType<CustomerDto>(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Get([FromRoute] int customer_id)
    {
        var customer = await appDbContext.Customers
            .Where(c => c.Id == customer_id)
            .Include(c => c.Sales)
            .FirstOrDefaultAsync();

        if (customer == null)
            return NotFound();

        return Ok(mapperService.ToDto(customer));
    }

    [HttpPost]
    [ProducesResponseType(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public async Task<IActionResult> Create([FromBody] NewCustomer newCustomer)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (await appDbContext.Customers.Where(c => c.AppUserId == user!.Id).AnyAsync())
            return Conflict("Аккаунт покупателя уже существует");

        var customer = new Customer
        {
            AppUserId = user!.Id,
            CompanyName = newCustomer.CompanyName,
            Address = newCustomer.Address,
            Phone = newCustomer.Phone,
            Email = newCustomer.Email
        };

        await appDbContext.Customers.AddAsync(customer);
        await appDbContext.SaveChangesAsync();

        return Created();
    }

    [HttpGet("me")]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType<CustomerDto>(StatusCodes.Status200OK)]
    public async Task<IActionResult> Get()
    {
        var customer = await appDbContext.Customers
            .Where(c => c.AppUser.UserName == User.Identity!.Name)
            .Include(c => c.Sales)
            .FirstOrDefaultAsync();

        return customer == null
            ? NotFound()
            : Ok(mapperService.ToDto(customer));
    }

    [HttpGet]
    [Authorize(Policy = "IsStaff")]
    [ProducesResponseType<CustomerDto>(StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAll([FromQuery] int? take, [FromQuery] int skip = 0)
    {
        var customers = appDbContext.Customers.OrderBy(c => c.Id).Skip(skip);

        if (take != null)
            customers = customers.Take(take ?? 0);

        return Ok(customers
            .Include(c => c.Sales)
            .Select(mapperService.ToDto));
    }
}

public record NewCustomer(
    string CompanyName,
    string Phone,
    string Address,
    string Email
);