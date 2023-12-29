#pragma once

#include <cstddef>

class ReferenceCounter
{
    int count; // Reference count
public:
    ReferenceCounter() : count(0) {};
    void increment()
    {
        count++;
    }
    int decrement()
    {
        return --count;
    }

    template <typename T> friend class SmartPointer;
};



template <typename T>
class SmartPointer
{
    // private instance variables for dumb pointer and ReferenceCounter
    T* ptr;
    ReferenceCounter * rc;

public:
    SmartPointer(T* p = NULL)
    {// smart pointer hold two :dum p, and pointer to rc

        // initialize dumb pointer
        // set up and increment reference counter
        ptr = p;
        rc = new ReferenceCounter;
        rc->increment();
        //initialize reference counter
    }

    // Copy constructor
    SmartPointer(const SmartPointer<T> &t)
    {
        // Copy the data and reference pointer
        // increment the reference count
        ptr = t.ptr;
        rc = t.rc;
        rc->increment();
    }

    // Destructor
    ~SmartPointer()
    {
        // Decrement the reference count
        // if reference become zero delete the data
        rc->decrement();
        if (rc->count == 0) {
            delete (ptr);
            delete (rc);
        }
    }

    T &operator*() const
    {
        // delegate
        return *ptr;
    }

    T *operator->() const
    {
        // delegate
        return ptr;
    }

    // Assignment operator
    SmartPointer<T> &operator=(const SmartPointer<T> &p)
    {
        if (this->ptr == p.ptr)
            return *this;
        p.rc->increment();
        this->rc->decrement();
        if (this->rc->count == 0){
            delete(this->rc);
            delete(this->ptr);
        }
        this->ptr = p.ptr;
        this->rc = p.rc;
        return *this;
        

        //define how the assignment operator works.
        // if u set one smart pointer to another

        // Deal with old SmartPointer that is being overwritten

        // Lookout for use-after-free bug here! It may cause undefined behavior

        // Copy data and reference pointer from parameter into this (similar to copy constructor)

        // return this SmartPointer
    }

    // return the number of different SmartPointers managing the current object
    int useCount() const
    {
        return rc->count;
    }

    // Check equal to nullptr
    bool operator==(std::nullptr_t rhs) const
    {
        return (this->ptr == rhs);
    }

    // Check not equal to nullptr
    bool operator!=(std::nullptr_t rhs) const
    {
        return (this->ptr != rhs);
    }

    // Check not equal to nullptr
    operator bool() const
    {
        return this != nullptr;
    }
};

