import React from 'react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

const variants = {
  h1: "font-display font-medium text-4xl md:text-5xl tracking-tight leading-[1.1]",
  h2: "font-display font-medium text-3xl md:text-4xl tracking-tight leading-[1.2]",
  h3: "font-display font-medium text-xl md:text-2xl tracking-tight",
  body: "font-sans text-base text-gray-600 leading-relaxed",
  small: "font-sans text-sm text-gray-500",
  label: "font-sans text-xs font-medium uppercase tracking-wider text-gray-500",
};

export const Text = ({ 
  as: Component = "p", 
  variant = "body", 
  className, 
  children, 
  animate = false,
  delay = 0 
}) => {
  const words = typeof children === 'string' ? children.split(" ") : [];
  const isString = typeof children === 'string';

  if (!animate || !isString) {
    return (
      <Component className={cn(variants[variant], className)}>
        {children}
      </Component>
    );
  }

  const container = {
    hidden: { opacity: 0 },
    visible: (i = 1) => ({
      opacity: 1,
      transition: { staggerChildren: 0.03, delayChildren: delay * i },
    }),
  };

  const child = {
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring",
        damping: 12,
        stiffness: 100,
      },
    },
    hidden: {
      opacity: 0,
      y: 10,
      transition: {
        type: "spring",
        damping: 12,
        stiffness: 100,
      },
    },
  };

  return (
    <motion.div
      style={{ overflow: "hidden", display: "inline-block" }} // visual fix
      variants={container}
      initial="hidden"
      animate="visible"
      className={cn(variants[variant], className, "flex flex-wrap gap-x-[0.25em]")} // gap for spaces
    >
      {words.map((word, index) => (
        <motion.span key={index} variants={child} className="inline-block">
          {word}
        </motion.span>
      ))}
    </motion.div>
  );
};





