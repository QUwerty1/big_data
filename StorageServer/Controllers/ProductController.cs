using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using StorageServer.Dto;
using StorageServer.Models;
using StorageServer.Services;

namespace StorageServer.Controllers
{
    [Route("product")]
    [ApiController]
    public class ProductController(
        AppDbContext appDbContext,
        UserManager<AppUser> userManager,
        MapperService mapperService
    ) : ControllerBase
    {
        [HttpGet]
        public async Task<IActionResult> GetAll()
        {
            return Ok(appDbContext.Products.Select(p => mapperService.ToDto(p)));
        }

        [HttpGet("{product_id}")]
        public async Task<IActionResult> Get([FromRoute] int product_id)
        {
            var product = await appDbContext.Products
                .Where(p => p.Id == product_id)
                .FirstOrDefaultAsync();

            return product != null 
                ? Ok(mapperService.ToDto(product)) 
                : NotFound();
        }

        [HttpPost]
        public async Task<IActionResult> Create([FromBody] ProductDto productDto)
        {
            var user = await userManager.FindByNameAsync(User.Identity!.Name!);

            if (user!.IsStaff == false)
                return Forbid();

            await appDbContext.AddAsync(mapperService.ToEntity(productDto));
            await appDbContext.SaveChangesAsync();

            return Created();
        }

        [HttpPut]
        public async Task<IActionResult> Update([FromBody] ProductDto productDto)
        {
            var user = await userManager.FindByNameAsync(User.Identity!.Name!);

            if (user!.IsStaff == false)
                return Forbid();

            appDbContext.Update(mapperService.ToEntity(productDto));
            await appDbContext.SaveChangesAsync();

            return Ok();
        }
    }
}
