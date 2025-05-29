<?php

use App\Http\Controllers\Api\V1\UserController;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\V1\AuthController;

Route::get('/', function () {
    return response()->json(['status' => 'API is Running!...']);
});

Route::get('/health/', function () {
    return response()->json(['status' => 'Server is Healthy!...']);
});

Route::prefix('v1')->group(function () {

    Route::prefix('auth')->group(function () {
        Route::post('/register', [AuthController::class, 'register']);
        Route::post('/login', [AuthController::class, 'login']);
        Route::post('/refresh', [AuthController::class, 'refresh']);
        Route::post('/validate-token', [AuthController::class, 'validateToken']);
        Route::get('/validate-token', [AuthController::class, 'validateToken']); // Specific method for Traefik

        Route::middleware('jwt.auth')->group(function () {
            Route::post('/logout', [AuthController::class, 'logout']);
        });
    });

    Route::middleware('jwt.auth')->group(function () {
        Route::get('/me', [UserController::class, 'me']);
    });
});
