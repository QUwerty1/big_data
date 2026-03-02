using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Identity.Client;

using StorageServer.Models;

namespace StorageServer.Controllers;

[Route("sale")]
[ApiController]
[Authorize]
public class SaleController(
    UserManager<AppUser> userManager,
    AppDbContext appDbContext
) : ControllerBase
{
    [HttpGet("all")]
    public async Task<IActionResult> GetAll()
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        return Ok(appDbContext.Sales.ToList());
    }

    [HttpGet("{sale_id}")]
    public async Task<IActionResult> Get([FromQuery] int sale_id)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        var sale = appDbContext.Sales.Where(s => s.Id == sale_id).FirstOrDefault();

        if (sale == null)
            return NotFound();

        return Ok(sale);
    }

    [HttpPost]
    public async Task<IActionResult> Create()
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        

        return Ok();
    }

    [HttpPut("{sale_id}")]
    public async Task<IActionResult> Update([FromQuery] int sale_id)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        return Ok();
    }

    [HttpDelete("{sale_id}")]
    public async Task<IActionResult> Delete([FromQuery] int sale_id)
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        if (user!.IsStaff == false)
            return Forbid();

        return Ok();
    }
}
