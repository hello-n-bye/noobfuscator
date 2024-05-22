local content = "Hello, world from Noobfuscator example!"

local exampleBoolean = true -- This will be changed to false

local function foo(...)
   return print(...)
end

local function changeOperation(operation)
   if (type(operation)) ~= "boolean" then
      return error("Invalid operation type")
   else
      return operation == not operation
   end
end

foo(changeOperation(exampleBoolean)); -- false
foo(content); -- "Hello, world from Noobfuscator example!"
