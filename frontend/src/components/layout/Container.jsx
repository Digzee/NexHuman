function Container({ children, className = "" }){
    return (
        <div className={`mx-auto w-full max-w-7x1 px-6 md:px-10 lg:px-16 ${className}`}
        >
            {children}
        </div>
    );
}

export default Container;