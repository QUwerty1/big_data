using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using StorageServer.Models;

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
            var token = tokenService.GenerateToken(loginBody.UserName);
            return Ok(token);
        }
        return Unauthorized();
    }

    [HttpPost("register")]
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
}

public record LoginBody(
    string UserName, string Password
);