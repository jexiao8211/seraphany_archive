# CSS Organization Guide

This document explains how CSS is organized in this project.

## 📁 Folder Structure

```
frontend/src/styles/
├── variables.css       # Design tokens (colors, spacing, fonts)
├── global.css          # Base styles, resets, typography
├── layout.css          # Layout utilities and grid systems
├── components/         # Component-specific styles
│   └── header.css      # Header component styles
└── pages/              # Page-specific styles
    ├── home.css        # Home page styles
    ├── products.css    # Products page styles
    ├── cart.css        # Cart page styles
    └── auth.css        # Login/Register page styles
```

## 🎨 Design Philosophy

### 1. **Separation of Concerns**
- All styles are in dedicated CSS files
- Components only contain JSX markup and logic
- No inline styles or Tailwind utility classes in components

### 2. **CSS Custom Properties (Variables)**
All design tokens are defined in `variables.css`:

```css
:root {
  /* Colors */
  --color-primary: #7c3aed;
  --color-primary-dark: #6d28d9;
  
  /* Spacing */
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  
  /* Typography */
  --font-size-base: 1rem;
  --font-weight-bold: 700;
}
```

### 3. **Semantic Class Names**
Class names describe what the element **is**, not how it looks:

✅ Good:
- `.home-hero` (describes: hero section of home page)
- `.cart-item` (describes: an item in the cart)
- `.auth-submit` (describes: submit button in auth form)

❌ Bad:
- `.bg-purple-600` (describes appearance, not meaning)
- `.text-xl-bold` (describes appearance, not meaning)

## 📝 How to Add Styles

### Adding Styles for a New Page

1. Create a new CSS file in `styles/pages/`:
   ```
   styles/pages/checkout.css
   ```

2. Write your styles using semantic class names:
   ```css
   .checkout-page {
     /* page styles */
   }
   
   .checkout-form {
     /* form styles */
   }
   ```

3. Import the file in `index.css`:
   ```css
   @import './styles/pages/checkout.css';
   ```

4. Use the classes in your component:
   ```tsx
   const CheckoutPage = () => (
     <div className="checkout-page">
       <form className="checkout-form">
         {/* form content */}
       </form>
     </div>
   )
   ```

### Adding Styles for a New Component

Same process, but create the file in `styles/components/` instead.

## 🎯 Naming Conventions

### Class Naming Pattern

```
[component/page]-[element]-[modifier?]
```

Examples:
- `.cart-item` - An item in the cart
- `.cart-item-image` - Image within a cart item
- `.cart-item-remove` - Remove button for cart item
- `.header-nav-link` - Navigation link in header
- `.auth-submit` - Submit button in auth forms

### CSS File Naming

- Use lowercase with hyphens
- Match the component/page name
- Examples: `header.css`, `cart-page.css`, `product-list.css`

## 🔄 Import Order in index.css

The order matters! Import in this sequence:

```css
/* 1. Variables first (so they're available everywhere) */
@import './styles/variables.css';

/* 2. Global base styles */
@import './styles/global.css';

/* 3. Layout utilities */
@import './styles/layout.css';

/* 4. Component styles */
@import './styles/components/header.css';

/* 5. Page styles */
@import './styles/pages/home.css';
@import './styles/pages/products.css';
@import './styles/pages/cart.css';
@import './styles/pages/auth.css';
```

## 💡 Tips & Best Practices

### 1. Use CSS Variables
Instead of hardcoding values:

❌ Bad:
```css
.button {
  background-color: #7c3aed;
  padding: 0.5rem 1rem;
}
```

✅ Good:
```css
.button {
  background-color: var(--color-primary);
  padding: var(--spacing-sm) var(--spacing-md);
}
```

### 2. Keep Styles DRY
Define common patterns in `layout.css`:

```css
/* In layout.css */
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Use in components */
<div className="flex-center">
  {/* content */}
</div>
```

### 3. Responsive Design
Use media queries in the CSS files:

```css
.home-features-grid {
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .home-features-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### 4. Component Scope
Prefix all classes with the component/page name to avoid conflicts:

```css
/* header.css */
.header { }
.header-logo { }
.header-nav { }
.header-nav-link { }

/* cart.css */
.cart-page { }
.cart-item { }
.cart-item-image { }
```

## 🚀 Benefits of This Approach

1. **Easy to Find**: All styles for a component are in one file
2. **Easy to Maintain**: Change colors/spacing in one place (variables)
3. **No Conflicts**: Semantic naming prevents class name collisions
4. **Beginner-Friendly**: Traditional CSS that's easy to understand
5. **Performance**: No runtime overhead from CSS-in-JS
6. **Separation**: Clean separation between markup and styling

## 📚 Further Reading

- [CSS Custom Properties (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [BEM Naming Convention](http://getbem.com/) (similar to our approach)
- [CSS Architecture](https://philipwalton.com/articles/css-architecture/)

