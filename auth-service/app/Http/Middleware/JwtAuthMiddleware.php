<?php

namespace App\Http\Middleware;

use App\Facades\JwtService;
use App\Traits\Api\V1\ApiResponse;
use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Symfony\Component\HttpFoundation\Response;

class JwtAuthMiddleware
{
    use ApiResponse;

    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $token = $request->bearerToken();

        Log::info('JWT authentication attempt', [
            'path' => $request->path(),
            'token' => $token ? substr($token, 0, 10) . '...' : null
        ]);

        if (!$token) {
            Log::warning('Access token is missing', [
                'path' => $request->path()
            ]);
            return $this->errorResponse('Access token is missing', 401);
        }

        $decoded = JwtService::validateToken($token, 'access');

        if (!$decoded) {
            Log::warning('Invalid or expired access token', [
                'path' => $request->path(),
                'token' => substr($token, 0, 10) . '...'
            ]);
            return $this->errorResponse('Invalid or expired token', 401);
        }

        Log::info('JWT authentication successful', [
            'path' => $request->path(),
            'user_id' => $decoded['sub'],
            'email' => $decoded['email']
        ]);

        // Optionally attach user info to the request
        $request->attributes->set('user_id', $decoded['sub']);
        $request->attributes->set('email', $decoded['email']);

        return $next($request);
    }
}
