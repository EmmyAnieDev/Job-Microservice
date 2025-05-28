<?php

namespace App\Http\Controllers\Api\V1;

use App\Facades\JwtService;
use App\Http\Controllers\Controller;
use App\Http\Requests\Api\V1\RegisterRequest;
use App\Http\Requests\Api\V1\LoginRequest;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use App\Traits\Api\v1\ApiResponse;
use Illuminate\Support\Facades\Log;

/**
 * Class AuthController
 *
 * Handles user authentication processes such as registration, login,
 * token refresh, and logout using JWT.
 */
class AuthController extends Controller
{
    use ApiResponse;

    /**
     * Register a new user.
     *
     * @param  RegisterRequest  $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function register(RegisterRequest $request)
    {
        try {
            Log::info('User registration attempt', ['email' => $request->email]);

            $user = User::create([
                'name'     => $request->name,
                'email'    => $request->email,
                'password' => Hash::make($request->password),
            ]);

            $accessToken = JwtService::createAccessToken($user->id, $user->email);
            $refreshToken = JwtService::createRefreshToken($user->id, $user->email);

            Log::info('User registered successfully', [
                'user_id' => $user->id,
                'email' => $user->email
            ]);

            return $this->successResponse([
                'name'     => $request->name,
                'email'    => $request->email,
                'access_token'  => $accessToken,
                'refresh_token' => $refreshToken,
            ], 'User registered successfully.', 201);
        } catch (\Exception $e) {
            Log::error('User registration failed', [
                'email' => $request->email,
                'error' => $e->getMessage()
            ]);

            return $this->errorResponse('Registration failed.', 500);
        }
    }

    /**
     * Log in an existing user and issue JWT tokens.
     *
     * @param  LoginRequest  $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function login(LoginRequest $request)
    {
        Log::info('User login attempt', ['email' => $request->email]);

        $user = User::where('email', $request->email)->first();

        if (!$user || !Hash::check($request->password, $user->password)) {
            Log::warning('Invalid login attempt', ['email' => $request->email]);
            return $this->errorResponse('Invalid credentials.', 401);
        }

        $accessToken = JwtService::createAccessToken($user->id, $user->email);
        $refreshToken = JwtService::createRefreshToken($user->id, $user->email);

        Log::info('User logged in successfully', [
            'user_id' => $user->id,
            'email' => $user->email
        ]);

        return $this->successResponse([
            'access_token'  => $accessToken,
            'refresh_token' => $refreshToken,
        ], 'Login successful.');
    }

    /**
     * Refresh JWT tokens using a valid refresh token.
     *
     * @param  Request  $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function refresh(Request $request)
    {
        $refreshToken = $request->bearerToken();

        Log::info('Token refresh attempt', ['token' => substr($refreshToken, 0, 10) . '...']);

        $decoded = JwtService::validateToken($refreshToken, 'refresh');

        if (!$decoded) {
            Log::warning('Invalid or expired refresh token', [
                'token' => substr($refreshToken, 0, 10) . '...'
            ]);
            return $this->errorResponse('Invalid or expired refresh token.', 401);
        }

        $accessToken = JwtService::createAccessToken($decoded['sub'], $decoded['email']);
        $newRefreshToken = JwtService::createRefreshToken($decoded['sub'], $decoded['email']);

        JwtService::revokeToken($refreshToken);

        Log::info('Token refreshed successfully', [
            'user_id' => $decoded['sub'],
            'email' => $decoded['email']
        ]);

        return $this->successResponse([
            'access_token'  => $accessToken,
            'refresh_token' => $newRefreshToken,
        ], 'Token refreshed successfully.');
    }

    /**
     * Log out a user by revoking their access token.
     *
     * @param  Request  $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function logout(Request $request)
    {
        $accessToken = $request->bearerToken();

        if ($accessToken) {
            Log::info('User logout attempt', ['token' => substr($accessToken, 0, 10) . '...']);
            JwtService::revokeToken($accessToken);
            Log::info('User logged out successfully', ['token' => substr($accessToken, 0, 10) . '...']);
        } else {
            Log::warning('Logout attempt with no token provided');
        }

        return $this->successResponse(null, 'Logged out successfully.');
    }


    /**
     * Validate token for Traefik ForwardAuth middleware
     * Returns user information as HTTP headers
     */
    public function validateToken(Request $request)
    {
        $authHeader = $request->header('Authorization');

        if (!$authHeader || !str_starts_with($authHeader, 'Bearer ')) {
            return $this->errorResponse('Unauthorized', 401);
        }

        $token = trim(str_replace('Bearer', '', $authHeader));
        $decoded = JwtService::validateToken($token);

        if (!$decoded) {
            return response('Invalid or revoked token', 401);
        }

        // Return simple text response with user info as headers
        // Traefik will forward these headers to the downstream service
        return response('OK', 200)
            ->header('X-User-Id', (string) $decoded['sub'])
            ->header('X-User-Email', $decoded['email'])
            ->header('X-Auth-Status', 'validated');
    }

}
