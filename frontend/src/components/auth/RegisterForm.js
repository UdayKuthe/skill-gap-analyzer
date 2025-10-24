import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { EyeIcon, EyeSlashIcon, CheckIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { useAuth } from '../../context/AuthContext';
import { cn, isValidEmail, validatePassword } from '../../utils';

const RegisterForm = () => {
  const navigate = useNavigate();
  const { register, isLoading } = useAuth();

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirm_Password: '',
  });
  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordValidation, setPasswordValidation] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: '',
      }));
    }

    // Validate password in real-time
    if (name === 'password') {
      setPasswordValidation(validatePassword(value));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    } else if (formData.username.trim().length < 2) {
      newErrors.username = 'Username must be at least 2 characters';
    }

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!isValidEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    const passwordCheck = validatePassword(formData.password);
    if (!passwordCheck.isValid) {
      newErrors.password = Array.isArray(passwordCheck.feedback) 
        ? passwordCheck.feedback[0] 
        : 'Password does not meet requirements';
    }

    if (!formData.confirm_Password) {
      newErrors.confirm_Password = 'Please confirm your password';
    } else if (formData.password !== formData.confirm_Password) {
      newErrors.confirm_Password = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    const userData = {
      full_name: formData.username.trim(),
      email: formData.email,
      password: formData.password,
      confirm_password: formData.confirm_Password,
    };

    const result = await register(userData);
    
    if (result.success) {
      navigate('/dashboard', { replace: true });
    }
  };

  const getPasswordStrengthColor = (strength) => {
    switch (strength) {
      case 'weak': return 'bg-error-500';
      case 'medium': return 'bg-warning-500';
      case 'strong': return 'bg-success-500';
      default: return 'bg-gray-300';
    }
  };

  const getPasswordStrengthText = (strength) => {
    switch (strength) {
      case 'weak': return 'Weak';
      case 'medium': return 'Medium';
      case 'strong': return 'Strong';
      default: return '';
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="mx-auto h-12 w-12 flex items-center justify-center bg-primary-600 rounded-xl">
            <svg
              className="w-8 h-8 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
              />
            </svg>
          </div>
          <h2 className="mt-6 text-center text-3xl font-bold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{' '}
            <Link
              to="/login"
              className="font-medium text-primary-600 hover:text-primary-500 transition-colors"
            >
              sign in to your existing account
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="username" className="label">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                autoComplete="username"
                required
                className={cn(
                  'input',
                  errors.username && 'input-error'
                )}
                placeholder="Enter your username"
                value={formData.username}
                onChange={handleChange}
              />
              {errors.username && (
                <p className="error-message">{String(errors.username)}</p>
              )}
            </div>

            <div>
              <label htmlFor="email" className="label">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className={cn(
                  'input',
                  errors.email && 'input-error'
                )}
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
              />
              {errors.email && (
                <p className="error-message">{String(errors.email)}</p>
              )}
            </div>

            <div>
              <label htmlFor="password" className="label">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  required
                  className={cn(
                    'input pr-12',
                    errors.password && 'input-error'
                  )}
                  placeholder="Create a strong password"
                  value={formData.password}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  )}
                </button>
              </div>
              
              {/* Password Strength Indicator */}
              {formData.password && passwordValidation && (
                <div className="mt-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Password strength:</span>
                    <span className={cn(
                      'font-medium',
                      passwordValidation.strength === 'weak' && 'text-error-600',
                      passwordValidation.strength === 'medium' && 'text-warning-600',
                      passwordValidation.strength === 'strong' && 'text-success-600'
                    )}>
                      {getPasswordStrengthText(passwordValidation.strength)}
                    </span>
                  </div>
                  <div className="mt-1 w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={cn(
                        'h-2 rounded-full transition-all duration-300',
                        getPasswordStrengthColor(passwordValidation.strength)
                      )}
                      style={{ width: `${(passwordValidation.score / 5) * 100}%` }}
                    />
                  </div>
                </div>
              )}
              
              {errors.password && (
                <p className="error-message">{String(errors.password)}</p>
              )}
            </div>

            <div>
              <label htmlFor="confirmPassword" className="label">
                Confirm Password
              </label>
              <div className="relative">
                <input
                  id="confirm_Password"
                  name="confirm_Password"
                  type={showConfirmPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  required
                  className={cn(
                    'input pr-12',
                    errors.confirm_Password && 'input-error'
                  )}
                  placeholder="Confirm your password"
                  value={formData.confirm_Password}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                >
                  {showConfirmPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  )}
                </button>
              </div>
              {errors.confirm_Password && (
                <p className="error-message">{String(errors.confirm_Password)}</p>
              )}
            </div>
          </div>

          {/* Password Requirements */}
          {passwordValidation && formData.password && (
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2">Password requirements:</h4>
              <ul className="space-y-1">
                {[
                  { check: formData.password.length >= 8, text: 'At least 8 characters' },
                  { check: /[A-Z]/.test(formData.password), text: 'One uppercase letter' },
                  { check: /[a-z]/.test(formData.password), text: 'One lowercase letter' },
                  { check: /\d/.test(formData.password), text: 'One number' },
                  { check: /[!@#$%^&*(),.?":{}|<>]/.test(formData.password), text: 'One special character' },
                ].map((requirement, index) => (
                  <li key={index} className="flex items-center text-sm">
                    {requirement.check ? (
                      <CheckIcon className="h-4 w-4 text-success-500 mr-2" />
                    ) : (
                      <XMarkIcon className="h-4 w-4 text-gray-400 mr-2" />
                    )}
                    <span className={requirement.check ? 'text-success-600' : 'text-gray-500'}>
                      {requirement.text}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={isLoading || (passwordValidation && !passwordValidation.isValid)}
              className={cn(
                'btn btn-primary w-full btn-lg',
                (isLoading || (passwordValidation && !passwordValidation.isValid)) && 'opacity-50 cursor-not-allowed'
              )}
            >
              {isLoading ? (
                <>
                  <div className="loading-spinner w-4 h-4 mr-2" />
                  Creating account...
                </>
              ) : (
                'Create account'
              )}
            </button>
          </div>

          <div className="text-center">
            <p className="text-xs text-gray-500">
              By creating an account, you agree to our{' '}
              <Link to="/terms" className="text-primary-600 hover:text-primary-500">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link to="/privacy" className="text-primary-600 hover:text-primary-500">
                Privacy Policy
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterForm;
