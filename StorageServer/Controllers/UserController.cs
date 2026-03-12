using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using StorageServer.Models;
using StorageServer.Services;

namespace StorageServer.Controllers;

[ApiController]
[Route("/user")]
public class UserController(
    TokenService tokenService,
    UserManager<AppUser> userManager,
    ILogger<UserController> logger,
    AppDbContext appDbContext
) : ControllerBase
{

    [HttpPost("login")]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType<string>(StatusCodes.Status200OK)]
    public async Task<IActionResult> Login([FromBody] LoginBody loginBody)
    {
        var user = await userManager.FindByNameAsync(loginBody.UserName);

        if (user == null)
        {
            return Unauthorized();
        }

        var signResult = await userManager.CheckPasswordAsync(user, loginBody.Password);

        if (signResult)
        {
            var token = await tokenService.GenerateTokenAsync(loginBody.UserName);
            return Ok(token);
        }

        return Unauthorized();
    }

    [HttpPost("register")]
    [ProducesResponseType(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> Register([FromBody] LoginBody loginBody)
    {
        var user = new AppUser
        {
            UserName = loginBody.UserName,
        };

        var result = await userManager.CreateAsync(user, loginBody.Password);

        if (result.Succeeded)
        {
            return Created();
        }

        foreach (var e in result.Errors)
        {
            logger.LogInformation(e.Description);
        }

        return Unauthorized();
    }

    [HttpGet("me")]
    [Authorize]
    public async Task<IActionResult> GetMe()
    {
        var user = await appDbContext.Users
            .Where(u => u.NormalizedUserName == User.Identity!.Name!.Normalize())
            .Include(u => u.Customer)
            .Include(u => u.Supplier)
            .FirstAsync();

        var userInfo = new UserInfo(
            user.Id,
            user.UserName!,
            user.IsStaff,
            user.Customer != null,
            user.Supplier != null
        );

        return Ok(userInfo);
    }
}

public record LoginBody(
    string UserName,
    string Password
);

public record UserInfo
(
    string Id,
    string UserName,
    bool IsStaff,
    bool IsCustomer,
    bool IsSupplier
);