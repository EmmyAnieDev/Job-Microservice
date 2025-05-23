<?php

namespace App\Http\Requests\Api\V1;

use Illuminate\Foundation\Http\FormRequest;

class RegisterRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize()
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'name'     => 'required|string|max:255',
            'email'    => 'required|string|email|unique:users,email',
            'password' => 'required|string|min:6|confirmed',
        ];
    }

    /**
     * Get custom error messages for validation rules.
     *
     * @return array<string, string>
     */
    public function messages(): array
    {
        return [
            'name.required'     => 'Name is required.',
            'name.string'       => 'Name must be a valid string.',
            'name.max'          => 'Name must not exceed 255 characters.',

            'email.required'    => 'Email is required.',
            'email.string'      => 'Email must be a valid string.',
            'email.email'       => 'Please enter a valid email address.',
            'email.unique'      => 'This email is already taken.',

            'password.required' => 'Password is required.',
            'password.string'   => 'Password must be a valid string.',
            'password.min'      => 'Password must be at least 6 characters long.',
            'password.confirmed' => 'Password confirmation does not match.',
        ];
    }
}
