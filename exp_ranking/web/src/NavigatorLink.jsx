import React from "react";

export default function NavigatorLink({
  href,
  children,
  className = "",
  onClick,
}) {
  if (!href) {
    return <span className={className}>{children}</span>;
  }

  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className={`hover:underline ${className}`}
      onClick={(event) => {
        event.stopPropagation();
        onClick?.(event);
      }}
    >
      {children}
    </a>
  );
}
