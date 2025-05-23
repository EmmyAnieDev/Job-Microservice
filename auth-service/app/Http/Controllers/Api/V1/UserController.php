<?php

namespace App\Http\Controllers\Api\V1;

use App\Facades\JwtService;
use App\Http\Controllers\Controller;
use App\Models\User;
use App\Traits\Api\v1\ApiResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class UserController extends Controller
{
    use ApiResponse;

    /**
     * Get the authenticated user's profile information.
     *
     * @param  Request  $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function me(Request $request)
    {
        $accessToken = $request->bearerToken();

        Log::info('User profile retrieval attempt', ['token' => substr($accessToken, 0, 10) . '...']);

        if (!$accessToken) {
            Log::warning('Profile retrieval attempt with no token provided');
            return $this->errorResponse('No token provided.', 401);
        }

        $decoded = JwtService::validateToken($accessToken, 'access');

        if (!$decoded) {
            Log::warning('Invalid or expired access token for profile retrieval', [
                'token' => substr($accessToken, 0, 10) . '...'
            ]);
            return $this->errorResponse('Invalid or expired token.', 401);
        }

        $user = User::find($decoded['sub']);

        if (!$user) {
            Log::error('User not found for profile retrieval', [
                'user_id' => $decoded['sub'],
                'email' => $decoded['email']
            ]);
            return $this->errorResponse('User not found.', 404);
        }

        Log::info('User profile retrieved successfully', [
            'user_id' => $user->id,
            'email' => $user->email
        ]);

        return $this->successResponse([
            'id' => $user->id,
            'name' => $user->name,
            'email' => $user->email,
            'created_at' => $user->created_at,
            'updated_at' => $user->updated_at,
        ], 'Profile retrieved successfully.');
    }
}
