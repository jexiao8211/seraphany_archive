/**
 * Cart context for managing shopping cart state
 * Persists cart to localStorage for cross-session persistence
 */
import React, { createContext, useContext, useReducer, useEffect } from 'react'
import type { ReactNode } from 'react'
import type { CartItem } from '../types'

const CART_STORAGE_KEY = 'seraphany_cart'

interface CartState {
  items: CartItem[]
}

interface CartContextType {
  items: CartItem[]
  addItem: (item: Omit<CartItem, 'quantity'>) => void
  removeItem: (id: number) => void
  updateQuantity: (id: number, quantity: number) => void
  clearCart: () => void
  getItemCount: () => number
  getTotalPrice: () => number
}

type CartAction =
  | { type: 'ADD_ITEM'; payload: Omit<CartItem, 'quantity'> }
  | { type: 'REMOVE_ITEM'; payload: number }
  | { type: 'UPDATE_QUANTITY'; payload: { id: number; quantity: number } }
  | { type: 'CLEAR_CART' }
  | { type: 'LOAD_CART'; payload: CartItem[] }

const CartContext = createContext<CartContextType | undefined>(undefined)

/**
 * Load cart from localStorage
 */
const loadCartFromStorage = (): CartItem[] => {
  try {
    const stored = localStorage.getItem(CART_STORAGE_KEY)
    if (stored) {
      const parsed = JSON.parse(stored)
      // Validate that it's an array of cart items
      if (Array.isArray(parsed)) {
        return parsed.filter(item => 
          typeof item.id === 'number' &&
          typeof item.name === 'string' &&
          typeof item.price === 'number' &&
          typeof item.quantity === 'number'
        )
      }
    }
  } catch (error) {
    console.error('Failed to load cart from localStorage:', error)
  }
  return []
}

/**
 * Save cart to localStorage
 */
const saveCartToStorage = (items: CartItem[]): void => {
  try {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items))
  } catch (error) {
    console.error('Failed to save cart to localStorage:', error)
  }
}

const cartReducer = (state: CartState, action: CartAction): CartState => {
  switch (action.type) {
    case 'LOAD_CART':
      return { ...state, items: action.payload }
    case 'ADD_ITEM': {
      const existingItem = state.items.find(item => item.id === action.payload.id)
      if (existingItem) {
        return {
          ...state,
          items: state.items.map(item =>
            item.id === action.payload.id
              ? { ...item, quantity: item.quantity + 1 }
              : item
          )
        }
      }
      return {
        ...state,
        items: [...state.items, { ...action.payload, quantity: 1 }]
      }
    }
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(item => item.id !== action.payload)
      }
    case 'UPDATE_QUANTITY':
      return {
        ...state,
        items: state.items.map(item =>
          item.id === action.payload.id
            ? { ...item, quantity: action.payload.quantity }
            : item
        ).filter(item => item.quantity > 0)
      }
    case 'CLEAR_CART':
      return { ...state, items: [] }
    default:
      return state
  }
}

export const CartProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(cartReducer, { items: [] })

  // Load cart from localStorage on mount
  useEffect(() => {
    const savedCart = loadCartFromStorage()
    if (savedCart.length > 0) {
      dispatch({ type: 'LOAD_CART', payload: savedCart })
    }
  }, [])

  // Save cart to localStorage whenever it changes
  useEffect(() => {
    saveCartToStorage(state.items)
  }, [state.items])

  const addItem = (item: Omit<CartItem, 'quantity'>) => {
    dispatch({ type: 'ADD_ITEM', payload: item })
  }

  const removeItem = (id: number) => {
    dispatch({ type: 'REMOVE_ITEM', payload: id })
  }

  const updateQuantity = (id: number, quantity: number) => {
    dispatch({ type: 'UPDATE_QUANTITY', payload: { id, quantity } })
  }

  const clearCart = () => {
    dispatch({ type: 'CLEAR_CART' })
  }

  const getItemCount = () => {
    return state.items.reduce((total, item) => total + item.quantity, 0)
  }

  const getTotalPrice = () => {
    return state.items.reduce((total, item) => total + (item.price * item.quantity), 0)
  }

  return (
    <CartContext.Provider
      value={{
        items: state.items,
        addItem,
        removeItem,
        updateQuantity,
        clearCart,
        getItemCount,
        getTotalPrice,
      }}
    >
      {children}
    </CartContext.Provider>
  )
}

export const useCart = () => {
  const context = useContext(CartContext)
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}
