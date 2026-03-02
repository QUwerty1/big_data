using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using StorageServer.DTO;
using StorageServer.Models;

namespace StorageServer.Controllers
{
    [Route("customer")]
    [ApiController]
    [Authorize]
    public class CustomerController(
        AppDbContext appDbContext,
        UserManager<AppUser> userManager
    ) : ControllerBase
    {
        [HttpGet("{customer_id}")]
        public async Task<IActionResult> GetCuStomerInfo([FromRoute] int customer_id)
        {
            var user = await userManager.FindByNameAsync(User.Identity!.Name!);

            if (user!.IsStaff == false)
                return Forbid();

            var customer = await appDbContext.Customers
                .FromSqlInterpolated($"SELECT * FROM Customers WHERE id = {customer_id}")
                .FirstOrDefaultAsync();

            if (customer == null)
                return NotFound();

            return Ok(new CustomerDTO(
                customer.CompanyName,
                customer.Phone,
                customer.Address,
                customer.Email,
                customer.Id,
                customer.AppUserId
            ));
        }

        [HttpPost]
        public async Task<IActionResult> CreateCustomer([FromBody] CustomerDTO customerDTO)
        {
            var user = await userManager.FindByNameAsync(User.Identity!.Name!);

            if (await appDbContext.Customers.Where(c => c.AppUserId == user!.Id).AnyAsync())
                return Conflict("Аккаунт покупателя уже существует");

            var customer = new Customer
            {
                CompanyName = customerDTO.CompanyName,
                Phone = customerDTO.Phone,
                Address = customerDTO.Address,
                Email = customerDTO.Email,
                Sales = [],
                AppUserId = user!.Id,
                AppUser = user
            };

            await appDbContext.Customers.AddAsync(customer);
            await appDbContext.SaveChangesAsync();

            return Created();
        }

        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var user = await userManager.FindByNameAsync(User.Identity!.Name!);

            if (user!.Customer == null)
                return NotFound();

            var customer = user.Customer;

            return Ok(new CustomerDTO(
                customer.CompanyName,
                customer.Phone,
                customer.Address,
                customer.Email
            ));
        }

        [HttpGet("all")]
        public async Task<IActionResult> GetAllAsync([FromQuery] int? take, [FromQuery] int skip = 0)
        {
            var user = await userManager.FindByNameAsync(User.Identity!.Name!);

            if (user!.IsStaff == false)
                return Forbid();

            var customers = appDbContext.Customers.Skip(skip);

            if (take != null)
            {
                customers = customers.Take(take ?? 0);
            }

            return Ok(customers.Select(c => new CustomerDTO(
                c.CompanyName,
                c.Phone,
                c.Address,
                c.Email,
                c.Id,
                c.AppUserId
            )));
        }
    }
}

