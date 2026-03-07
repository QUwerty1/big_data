using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

using StorageServer.Models;
using StorageServer.Services;

namespace StorageServer.Controllers;

[ApiController]
[Route("/user")]
public class UserController(
    TokenService tokenService,
    UserManager<AppUser> userManager,
    ILogger<UserController> logger
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

    [HttpGet("is_staff")]
    [Authorize]
    public async Task<bool> IsStaff()
    {
        var user = await userManager.FindByNameAsync(User.Identity!.Name!);

        return user!.IsStaff;
    }
}

public record LoginBody(
    string UserName,
    string Password
);