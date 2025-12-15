import React from 'react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export const Button = ({
  children,
  className,
  variant = 'primary',
  disabled,
  onClick,
  type = 'button',
  icon: Icon,
  ...props
}) => {
  const baseStyles = "relative inline-flex items-center justify-center rounded-xl font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none";
  
  const variants = {
    primary: "bg-gray-900 text-white hover:bg-black shadow-lg shadow-gray-900/20 active:scale-95",
    secondary: "bg-white text-gray-900 border border-gray-200 hover:bg-gray-50 hover:border-gray-300 shadow-sm active:scale-95",
    ghost: "text-gray-600 hover:text-gray-900 hover:bg-gray-100 active:scale-95",
    glass: "bg-white/80 backdrop-blur-md border border-white/20 text-gray-900 shadow-sm hover:bg-white/90 active:scale-95",
  };

  const sizes = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-[15px]",
    lg: "px-6 py-3 text-base",
    icon: "p-2",
  };

  const size = props.size || 'md';

  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={cn(baseStyles, variants[variant], sizes[size], className)}
      disabled={disabled}
      onClick={onClick}
      type={type}
      {...props}
    >
      {Icon && <Icon className={cn("w-4 h-4", children && "mr-2")} />}
      {children}
    </motion.button>
  );
};





