<?php

namespace App\Providers;

use App\Services\V1\JwtService;
use Illuminate\Support\ServiceProvider;

class JwtServiceProvider extends ServiceProvider
{
    public function register()
    {
        $this->app->singleton(JwtService::class, function ($app) {
            return new JwtService();
        });
    }

    public function boot()
    {
        $this->app->alias(JwtService::class, 'JwtService');
    }
}
